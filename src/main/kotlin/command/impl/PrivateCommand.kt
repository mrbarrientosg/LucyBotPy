package command.impl

import Lucy
import command.Command
import discord4j.core.event.domain.message.MessageCreateEvent
import kotlinx.coroutines.reactive.awaitSingle
import reactor.core.publisher.Mono

enum class PrivateCommands {
    CREATE,
    INVITE,
    REMOVE
}

class PrivateCommand: Command() {

    init {
        subCommands[PrivateCommands.CREATE.name] = this::create
    }

    fun create(event: MessageCreateEvent, bot: Lucy, args: Array<String>): Mono<Void> {
        return Mono.create {
            val channel = event.message.channel.block()
            channel.createMessage("create").block()
        }
    }

    override fun execute(event: MessageCreateEvent, bot: Lucy, args: Array<String>): Mono<Void> {
        val first = args.firstOrNull()

        first?.let {
            if (subCommands.contains(it.toUpperCase())) {
                val params = args.toMutableList()
                params.removeAt(0)
                return subCommands[it.toUpperCase()]!!.invoke(event, bot, params.toTypedArray())
            }
        }

        return Mono.create {
            val channel = event.message.channel.block()
            channel.createMessage("Holi").block()
        }
    }
}