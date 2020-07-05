package command

import Lucy
import discord4j.core.`object`.entity.Message
import discord4j.core.event.domain.message.MessageCreateEvent
import reactor.core.publisher.Mono

typealias CommandCallback = (event: MessageCreateEvent, bot: Lucy, args: Array<String>) -> Mono<Void>

abstract class Command {

    protected val subCommands: HashMap<String, CommandCallback> = hashMapOf()

    private var _info: CommandInfo = CommandInfo("", "", "", arrayListOf(), arrayListOf(), false)

    public var info: CommandInfo
        get() = this._info
        set(value) {
            this._info = value
        }

    fun check(prefix: String, command: String): Boolean = command.startsWith(prefix + _info.name)

    abstract fun execute(event: MessageCreateEvent, bot: Lucy, args: Array<String>): Mono<Void>

    open fun canUse(message: Message): Mono<Boolean> {
        return Mono.just(true)
    }
}
