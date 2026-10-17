// Fixture: non-conforming Swift
func viewDidLoad() {
    manager.startUpdatingLocation()
    Timer.scheduledTimer(withTimeInterval: 5, repeats: true) { _ in refresh() }
    DispatchQueue.main.sync { update() }
    let data = try Data(contentsOf: url)
    let session = URLSession(configuration: .default)
}
