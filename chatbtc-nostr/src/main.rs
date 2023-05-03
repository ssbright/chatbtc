// Bot that reacts to '!yes', '!no' and '!results' commands.
use nostr_bot::*;
use std::env;
use std::path::PathBuf;





// Your struct that will be passed to the commands responses
struct Votes {
    question: String,
    yes: u64,
    no: u64,
}

type State = nostr_bot::State<Votes>;

fn format_results(question: &str, votes: &Votes) -> String {
    format!(
        "{}\n------------------\nyes: {}\nno:  {}",
        question, votes.yes, votes.no
    )
}

// Following functions are command responses, you are getting nostr event
// and shared state as arguments and you are supposed to return non-signed
// event which is then signed using the bot's key and send to relays
async fn yes(event: Event, state: State) -> EventNonSigned {
    let mut votes = state.lock().await;
    votes.yes += 1;

    // Use formatted voting results to create new event
    // that is a reply to the incoming command
    get_reply(event, format_results(&votes.question, &votes))
}

async fn no(event: Event, state: State) -> EventNonSigned {
    let mut votes = state.lock().await;
    votes.no += 1;
    get_reply(event, format_results(&votes.question, &votes))
}

async fn results(event: Event, state: State) -> EventNonSigned {
    let votes = state.lock().await;
    get_reply(event, format_results(&votes.question, &votes))
}

#[tokio::main]
async fn main() {
    init_logger();

    let mut path = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    path.push("..");
    path.push(".env");


    // Load environment variables from the specified path
    dotenv::from_path(&path).expect("Failed to load .env file");
    dotenv::dotenv().ok();


    let relays = vec![
        "wss://nostr-pub.wellorder.net",
        "wss://relay.damus.io",
        "wss://relay.nostr.info",
    ];
    let privkey: String = env::var("PRIVKEY").expect("DATABASE_URL not set"); // Changed type to String
    let keypair = keypair_from_secret(&privkey);

    let intro = String::from("I am online!");

    // Wrap your object into Arc<Mutex> so it can be shared among command handlers
    let shared_state = wrap_state(Votes {
        question: intro.clone(),
        yes: 0,
        no: 0,
    });

    // And now the Bot
    Bot::new(keypair, relays, shared_state)
        // You don't have to set these but then the bot will have incomplete profile info :(
        .name("ChatBTC")
        .about("A bot in development....")
        .picture("https://themindfulinquisitor.com/wp-content/uploads/2023/05/2023-05-02-14.26.34.jpg")
        //.intro_message(&intro)
        // You don't have to specify any command but then what will the bot do? Nothing.
        .command(Command::new("!yes", wrap!(yes)))
        .command(Command::new("!no", wrap!(no)))
        .command(Command::new("!results", wrap!(results)))
        // And finally run it
        .run()
        .await;
}