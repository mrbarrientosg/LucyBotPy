import command.Commands
import discord4j.core.DiscordClient
import discord4j.core.GatewayDiscordClient
import discord4j.core.`object`.entity.User
import discord4j.core.event.domain.message.MessageCreateEvent
import kotlinx.coroutines.reactor.mono
import reactor.core.publisher.Mono


class Lucy(prefix: String) {

    private val commands: Commands

    public var client: DiscordClient?
        private set

    init {
        this.commands = Commands(prefix)
        this.client = null
    }

    public fun run(token: String) {
        this.client = DiscordClient.create(token)
        commandHandler()
    }

    private fun commandHandler() {
        this.client?.let { it ->
            it.withGateway {
               mono {
                   it.on(MessageCreateEvent::class.java)
                       .flatMap { event ->
                           if (event.message.author.map(User::isBot).orElse(true)) {
                                return@flatMap Mono.just(false)
                           }
                           // TODO: Mejorar la forma en que se obtienen los argumentos del canal
                           return@flatMap Mono.just(event.message.content)
                                   .flatMap { content ->
                                       val args = content.split(" ").toMutableList()
                                       args.removeAt(0)

                                       val command = commands.handler(content)
                                       command?.execute(event, this@Lucy, args.toTypedArray()) ?: throw RuntimeException()
                                   }
                       }.doOnError { error ->
                           println(error)
                       }.subscribe()
               }
           }.block()
        }
    }
}