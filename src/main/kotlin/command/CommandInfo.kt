package command
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class CommandInfo(val name: String,
                       val description: String,
                       val help: String,
                       @SerialName("sub_commands") val subCommands: ArrayList<CommandInfo>,
                       val alias: ArrayList<String>,
                       @SerialName("is_group") val isGroup: Boolean)
