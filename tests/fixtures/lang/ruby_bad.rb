# Fixture: non-conforming Ruby
User.all.each { |u| puts u.name }
names = User.where(active: true).map(&:name)
puts "x" if Order.count > 0
items.each do |i|
  next if blocked.include?(i)
end
Rails.cache.fetch("k") { compute }
