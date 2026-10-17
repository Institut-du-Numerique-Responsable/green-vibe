// Fixture: non-conforming Rust
async fn handle(items: Vec<String>) -> usize {
    let client = reqwest::Client::new();
    std::thread::sleep(std::time::Duration::from_secs(1));
    let n: Vec<usize> = items.iter().map(|s| s.len()).collect::<Vec<usize>>().into_iter().collect();
    for s in &items { let _owned = s.clone(); }
    let first = items.first().unwrap();
    n.len() + first.len()
}
