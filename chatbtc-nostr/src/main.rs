extern crate dotenv;

use std::env;
use std::path::PathBuf;
use nostr_sdk::prelude::*;
use std::str::FromStr;
use nostr_sdk::message::subscription::Filter;
use std::error::Error as _;
use std::time::Duration;
use tokio::time;







#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut path = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    path.push("..");
    path.push(".env");

    // Load environment variables from the specified path
    dotenv::from_path(&path).expect("Failed to load .env file");
    dotenv::dotenv().ok();

    // Access environment variables
    let privkey: String = env::var("PRIVKEY").expect("DATABASE_URL not set"); // Changed type to String
    let secret_key = SecretKey::from_str(&privkey).unwrap();
    let my_keys = Keys::new(privkey.parse()?);


    let client = Client::new(&my_keys);
    client.add_relay("wss://relay.house", None).await?;
    client.add_relay("wss://relay.damus.io", None).await?;
    client.connect().await;


    let message = format!("Hello, nostr! My public key is: {}", my_keys.public_key().to_string());
    println!("{}", message);

    let event_id: EventId = client.publish_text_note(message, &[]).await?;
    println!("{:#?}", event_id);


    // Use event_id in the Filter struct
    let filter: Filter = Filter::new().id(event_id);
    //Since we are sending the subscription filter to the relay immediately after posting our message,  let's add a 1 second sleep
    time::sleep(Duration::from_secs(1)).await;
    //Then send the Filter to the relay via the client to retrieve a list of events that match that criteria.
    let events: Vec<Event> = client.get_events_of(vec![filter], None).await?;
    println!("{:#?}", events);


    Ok(())
}
