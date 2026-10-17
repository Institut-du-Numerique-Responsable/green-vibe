# Fixture: non-conforming Julia
function step()
    global counter
    counter += 1
end
out = Float64[]
for i in 1:n
    push!(out, i * 2.0)
end
Threads.@threads for i in 1:n
    work(i)
end
