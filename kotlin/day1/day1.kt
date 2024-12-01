import java.io.File
import java.io.FileReader
import kotlin.math.abs

fun pt1(lines: List<String>): Int {
    val A = mutableListOf<Int>()
    val B = mutableListOf<Int>()
  for (line in lines) {
    val (a, b) = line.split("   ")
    A.add(a.toInt())
    B.add(b.toInt())

  }
  val ans = A.sorted().zip(B.sorted()) { a, b -> 
    abs(a - b)
  }.sum()
  println(ans)

    return 0
}

fun pt2(lines: List<String>): Int {
    val A = mutableListOf<Int>()
    val B = mutableMapOf<Int, Int>()
  for (line in lines) {
    val (a, b) = line.split("   ")
    A.add(a.toInt())
    if (b.toInt() in B.keys) {
      B[b.toInt()] = B[b.toInt()]!! + 1
    } else {
      B[b.toInt()] = 1
    }

  }
  val ans = A.map { it * B.getOrDefault(it, 0) }.sum()
  println(ans)
  return ans

}

fun main() {
    val input = FileReader(File("../../inputs/day1.txt")).readLines()
    println(pt1(input))
    println(pt2(input))
}
