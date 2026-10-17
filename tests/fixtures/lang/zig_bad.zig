// Fixture: non-conforming Zig
fn load(allocator: std.mem.Allocator, reader: anytype) ![]u8 {
    const buf = try allocator.alloc(u8, 1024);
    _ = buf;
    return try reader.readAllAlloc(allocator, 1 << 30);
}
