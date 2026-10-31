
import org.arl.fjage.*
import org.arl.unet.*

class EchoAgent extends UnetAgent {

    @Override
    void startup() {
        // Listen for incoming datagrams
        subscribe topic(Topics.DATAGRAM)

        println "EchoAgent started and listening..."
    }

    @Override
    void processMessage(Message msg) {

        // Accept only USER protocol datagrams
        if (msg instanceof DatagramNtf &&
            msg.protocol == Protocol.USER) {

            // Convert received bytes into text
            String receivedText = new String(msg.data)

            // Convert text to uppercase
            String upperText = receivedText.toUpperCase()

            // Get reception time
            String receptionTime = new Date().toString()

            // Append reception time
            String replyText = upperText +
                               " | Received at: " +
                               receptionTime

            println "Received: ${receivedText}"
            println "Replying: ${replyText}"

            // Send reply to original sender using DATA protocol
            send new DatagramReq(
                recipient: msg.sender,
                to: msg.from,
                protocol: Protocol.DATA,
                data: replyText.bytes
            )
        }
    }
}
