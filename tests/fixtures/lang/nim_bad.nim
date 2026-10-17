# Fixture: non-conforming Nim
proc total(xs: seq[int]): int =
  for x in xs: result += x
let f = open("data.txt")
echo f.readAll()
f.close()
