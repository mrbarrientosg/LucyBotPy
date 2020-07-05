package command

import command.impl.PrivateCommand
import kotlinx.serialization.builtins.list
import kotlinx.serialization.json.*
import java.io.File

class Commands {

    private val _prefix: String
    public val prefix: String
        get() = this._prefix

    private val commands: HashMap<String, Command>

    constructor(prefix: String) {
        this._prefix = prefix
        this.commands = HashMap()
        setupCommands()
        readCommands()
    }

    public fun handler(content: String): Command? {
        var command: Command? = null

        this.commands.forEach {
            if (it.value.check(_prefix, content)) {
                command = it.value
                return command
            }
        }

        return command
    }

    private fun setupCommands() {
        this.commands.put(CommandsType.PRIVATE.type, PrivateCommand())
    }

    private fun readCommands() {
        val json = Json(JsonConfiguration.Stable)
        val options = File("src/main/resources/lucy_options.json").readText()
        val cmd = json.parseJson(options).jsonObject["commands"]

        json.parse(CommandInfo.serializer().list, cmd.toString())
            .forEach {
                if (this.commands.contains(it.name)) {
                    this.commands[it.name]?.let { command ->
                        command.info = it
                    }
                }
            }
    }

    override fun toString(): String {
        var output: String = ""
        this.commands.forEach {
            output += it.key + ":\n"
            //output += it.value.subCommands.joinToString("\n\t", "\t")
        }

        return output
    }


}