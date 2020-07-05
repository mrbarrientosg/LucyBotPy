import discord4j.core.DiscordClient
import discord4j.core.event.domain.message.MessageCreateEvent
import kotlinx.coroutines.reactive.asFlow
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.reactive.awaitSingle
import kotlinx.coroutines.reactor.mono
import kotlinx.serialization.*
import kotlinx.serialization.json.*
import java.io.File

@ImplicitReflectionSerializer
fun main(args: Array<String>) {

    val bot = Lucy(prefix = "lt:")

    bot.run("NzI3MDAyMDcxMzQ5MzI5OTMw.Xvlffg.Q9cI34neuqdKhW7aeQAP4abFKYw")
}

