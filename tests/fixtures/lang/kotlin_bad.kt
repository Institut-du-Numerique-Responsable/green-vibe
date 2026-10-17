// Fixture: non-conforming Kotlin
fun start() {
    GlobalScope.launch { refresh() }
    runBlocking { load() }
    val ch = Channel<Int>(Channel.UNLIMITED)
    val r = list.map { it * 2 }.filter { it > 3 }.map { it + 1 }
}
