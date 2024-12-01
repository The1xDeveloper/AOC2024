import java.io.File
import java.io.FileReader

fun pt1(lines: List<String>): Int {
    lines.forEach {
        println(it)
    }
    return 0
}

fun pt2(lines: List<String>): Int {
    lines.forEach {
        println(it)
    }
    return 0
}

fun main() {
    val input = FileReader(File("../../inputs/day.txt")).readLines()
    println(pt1(input))
    println(pt2(input))
}
