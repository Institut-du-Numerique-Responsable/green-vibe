// Fixture: non-conforming C#
public class Repo {
    static Dictionary<string, object> Cache = new();
    public void Run() {
        var rows = db.Orders.ToList().Where(o => o.Total > 10);
        var x = db.Orders.Include(o => o.Lines).Include(o => o.Customer);
        if (rows.Count() > 0) { }
        var r = GetAsync().Result;
        var http = new HttpClient();
        _logger.LogInformation($"rows {rows}");
        while (!stop) { DoWork(); Task.Delay(500); }
    }
}
