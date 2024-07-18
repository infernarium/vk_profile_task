using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

namespace bestsellers
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                var topSellers = GetTopSellers();
                if (topSellers.Count == 0)
                {
                    Console.WriteLine("Что-то пошло не по плану. Возможно, недоступен сервер со статистикой.");
                }
                else
                {
                    foreach (var game in topSellers)
                    {
                        Console.WriteLine(game);
                    }
                }
            }
            catch (WebDriverException wdEx)
            {
                Console.WriteLine($"Произошла ошибка при работе с WebDriver: {wdEx.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Произошло исключение: {ex.Message}");
            }
        }

        private static List<Game> GetTopSellers()
        {
            List<Game> topSellers = new List<Game>(10);

            var options = new ChromeOptions();
            options.AddArgument("--headless");
            using IWebDriver driver = new ChromeDriver(options);

            try
            {
                driver.Navigate().GoToUrl("https://store.steampowered.com/charts/topselling/RU");
                Thread.Sleep(5000);

                var gameElements = driver.FindElements(By.ClassName("_2-RN6nWOY56sNmcDHu069P"));
                for (int i = 0; i < Math.Min(gameElements.Count, 10); i++)
                {
                    var gameElement = gameElements[i];

                    string name = gameElement.FindElement(By.ClassName("_1n_4-zvf0n4aqGEksbgW9N")).Text;
                    string price = gameElement.FindElement(By.ClassName("_3j4dI1yA7cRfCvK8h406OB")).Text;

                    topSellers.Add(new Game(name, price, i + 1));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка при получении данных: {ex.Message}");
            }
            finally
            {
                driver.Quit();
            }
            return topSellers;
        }
    }
     
    class Game
    {
        public string Name { get; set; }
        public string Price { get; set; }
        public int Place { get; set; }
        public Game(string name, string price, int place)
        {
            Name = name;
            Price = price;
            Place = place;
        }
        public override string ToString()
        { 
            return $"{Place} - {Name} - {Price}";
        }
    }
}