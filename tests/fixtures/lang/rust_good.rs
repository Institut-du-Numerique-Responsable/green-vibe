// Fixture: conforming Rust
use std::sync::OnceLock;
static CLIENT: OnceLock<reqwest::Client> = OnceLock::new();

async fn handle(items: &[String]) -> Result<usize, String> {
    let _client = CLIENT.get_or_init(reqwest::Client::new);
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    let total: usize = items.iter().map(|s| s.len()).sum();
    let first = items.first().ok_or("empty")?;
    Ok(total + first.len())
}
