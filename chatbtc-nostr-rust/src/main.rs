extern crate dotenv;

use std::env;
use std::path::PathBuf;
use nostr_sdk::prelude::*;
use std::str::FromStr;
use nostr_sdk::message::subscription::Filter;
use std::error::Error as _;
use std::time::Duration;
use tokio::time;
use nostr_bot::Bot;



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
    //let secret_key = SecretKey::from_str(&privkey).unwrap();
    let my_keys = Keys::new(privkey.parse()?);



    //Relays for NDK
    let client = Client::new(&my_keys);
    client.add_relay("wss://relay.house", None).await?;
    client.add_relay("wss://relay.damus.io", None).await?;
    client.connect().await;


    let personal_pubkey = XOnlyPublicKey::from_bech32(
        "npub1249tdlkkwkv966uek7dd0duyl7x2ffdsyaugztsedrhwp3ktcflq66ys0r",
    )
        .unwrap();

    client
        .send_direct_msg(personal_pubkey, "My first DM from Nostr SDK!")
        .await
        .unwrap();


    Ok(())
}
