// Import the package
import NDK from "@nostr-dev-kit/ndk";

async function main() {
  const ndk = new NDK({ explicitRelayUrls: ["wss://relay.house", "wss://relay.damus.io"] });
  await ndk.connect();

  console.log('Hello, world!');
}

main();



