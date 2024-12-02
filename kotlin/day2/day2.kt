import java.io.File
import java.io.FileReader
import kotlin.math.abs

private fun testNums(nums: List<Int>): Boolean {
    val diffs =
        nums.windowed(2).map {
            it.first() - it.last()
        }
    val isMonoInc = diffs.all { it > 0 }
    val isMonoDec = diffs.all { it < 0 }
    val isInBounds = diffs.all { 1 <= abs(it) && abs(it) <= 3 }
    return (isMonoInc || isMonoDec) && isInBounds
}

fun pt1(lines: List<String>): Int =
    lines
        .map { line ->
            val nums = line.split(" ").map { it.toInt() }
            if (testNums(nums)) 1 else 0
        }.sum()

fun pt2(lines: List<String>): Int =
    lines
        .map { line ->
            val nums = line.split(" ").map { it.toInt() }
            val subNums =
                nums.mapIndexed { i, _ ->
                    nums.filterIndexed { idx, _ -> idx != i }
                }
            if (testNums(nums) || subNums.any { testNums(it) }) 1 else 0
        }.sum()

fun main() {
    val input = FileReader(File("../../inputs/day2.txt")).readLines()
    println(pt1(input))
    println(pt2(input))
}
