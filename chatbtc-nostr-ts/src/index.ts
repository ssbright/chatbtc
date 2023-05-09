// Import the package
import NDK, { NDKPrivateKeySigner, NDKEvent } from "@nostr-dev-kit/ndk";
import {config} from "dotenv";
import * as path from 'path';

const envPath = path.join(__dirname, '../..', '.env');
config({ path: envPath });

async function main() {
    const pubkey = process.env.PUBKEY;
    const privkey = process.env.PRIVKEY;


  const ndksigner = new NDKPrivateKeySigner(privkey);
  const ndk = new NDK({ explicitRelayUrls: ["wss://relay.house", "wss://relay.damus.io"], signer: ndksigner });
  await ndk.connect();


  const ndkEvent = new NDKEvent(ndk);
  ndkEvent.kind = 1;
  ndkEvent.content = "Hello again, world!";
  ndkEvent.publish(); // This will trigger the extension to ask the user to confirm signing.
}

main();



