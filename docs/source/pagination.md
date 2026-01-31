# Pagination

For endpoints returning a paginated response, the list of items are wrapped in a {class}`PaginatedList <clash_royale.PaginatedList>` class which makes working with pagination more Pythonic while doing the necessary API calls transparently.

## Controlling Results

### The `limit` Parameter

The `limit` parameter controls the **maximum total number of items** to fetch across all pages:

```python
# Fetch at most 50 players
players = client.leaderboards.get(leaderboard_id, limit=50)
for player in players:  # Safe: will only iterate over 50 players max
    print(player.name)
```

Without a `limit`, iteration will fetch **all available items** (potentially thousands):

```python
# ⚠️ Warning: No limit = fetches ALL pages!
players = client.leaderboards.get(leaderboard_id)
for player in players:  # Could make hundreds of API requests!
    print(player.name)
```

**Recommendation:** Always set a `limit` unless you genuinely need all results.

### The `page_size` Parameter

The `page_size` parameter controls how many items are fetched per API request (default: 100):

```python
# Fetch 500 players using pages of 250 items (2 API requests)
players = client.leaderboards.get(leaderboard_id, limit=500, page_size=250)
```

**When to adjust `page_size`:**
- **Large result sets** (500+ items): Increase to 250-1000 to reduce API calls
- **Need first result fast**: Decrease to 10-50 to get initial results quickly

## Iterating over Elements

The class is an iterator, meaning you can go through instances in the list with a for loop, or by calling `next()` to get the following item:

```python
players = client.leaderboards.get(leaderboard_id, limit=100)

# Iterable style
for player in players:
    print(player.name)

# Iterator
player_1 = next(players)
player_2 = next(players)
player_3 = next(players)
```

This will take care of fetching extra pages if needed. Once all the elements have been fetched (or the `limit` is reached), no further network calls will happen. This will work if you iterate over the same paginated response again:

```python
# No API calls: players is reused from above
for player in players:
    print(player.name)
```

However, API calls would be repeated if you get a fresh paginated response:

```python
# New API calls: get() returns a fresh paginated list
for player in client.leaderboards.get(leaderboard_id, limit=100):
    print(player.name)
```

Be mindful of that when writing your code otherwise you'll consume your API quota quickly!

## Total Number

To get the total number of items fetched (respecting the `limit`), use the built-in `len()` on the materialized list:

```python
players = client.leaderboards.get(leaderboard_id, limit=50)
player_list = list(players)
print(len(player_list))  # 50 (or fewer if less available)
```

Note: The Clash Royale API does not provide a total count in advance, so you must fetch items to know how many there are.

## Indexing

You can access elements by index:

```python
players = client.leaderboards.get(leaderboard_id, limit=100)
second_player = players[1]
tenth_player = players[9]
```

Beware that accessing a large index may produce extra network calls to the Clash Royale API as pages preceding the given index will be fetched. For example, assuming the page size is 100, this will perform 2 API calls:

```python
players = client.leaderboards.get(leaderboard_id)
players[150]  # Fetches first 2 pages
```

If the index exceeds the `limit` or available items, an `IndexError` will be raised, as if it were a list. Unlike list, this feature doesn't support negative values at the time.

## Slicing

Slicing is supported and provides an easy way to get a specific range of results:

```python
players = client.leaderboards.get(leaderboard_id)

# With start & end
players[2:5]  # Players at positions 2, 3, 4

# Without start (get first N)
players[:10]  # Top 10 players

# Without end (get from position onwards)
players[10:]  # All players from position 10 onwards

# With start, end & step
players[0:20:2]  # Every other player in top 20
```

**Tip:** Slicing without an end (e.g., `players[10:]`) will fetch all remaining items, which could produce many API calls. Consider setting a `limit` first:

```python
# Safe: limit total results first, then slice
players = client.leaderboards.get(leaderboard_id, limit=100)
top_10 = players[:10]
```

## Best Practices

### ✅ DO

```python
# Set explicit limits
players = client.leaderboards.get(lb_id, limit=50)

# Use slicing for subsets
top_10 = players[:10]

# Use fetch() for clarity
top_50 = client.clans.search(name="Legend").fetch(50)

# Break early in loops
for player in players:
    if player.score > 5000:
        break
```

### ❌ DON'T

```python
# Don't fetch everything without a limit
players = client.leaderboards.get(lb_id)
all_players = list(players)  # Danger: could be thousands!

# Don't use tiny page sizes for large fetches
players = client.leaderboards.get(lb_id, limit=1000, page_size=10)  # 100 API requests!

# Don't ignore pagination when you only need a few items
for i, player in enumerate(client.leaderboards.get(lb_id)):
    if i >= 10:
        break
# Better: players = client.leaderboards.get(lb_id, limit=10)
```

## Performance Considerations

The number of API requests is calculated as: `ceil(limit / page_size)`

```python
# Examples:
# limit=50, page_size=100  → 1 request
# limit=150, page_size=100 → 2 requests
# limit=500, page_size=250 → 2 requests
# limit=1000, page_size=100 → 10 requests
```

Optimize by:
1. Setting appropriate `limit` values (don't fetch more than you need)
2. Increasing `page_size` for large bulk operations
3. Using slicing/`fetch()` to get exact counts
4. Reusing paginated lists instead of re-fetching

## Complete Example

```python
import clash_royale

client = clash_royale.Client(api_key="your_api_key")

# Get top 50 players efficiently
players = client.leaderboards.get(
    leaderboard_id=170000008,
    limit=50,
    page_size=50  # Single API request
)

# Work with top 10
top_10 = players.fetch(10)
for i, player in enumerate(top_10, 1):
    print(f"{i}. {player.name} - {player.score} points")

# Or use slicing
next_10 = players[10:20]
print(f"Players 11-20: {[p.name for p in next_10]}")

# Search clans with limit
clans = client.clans.search(name="Legend", min_members=40, limit=25)
for clan in clans:
    print(f"{clan.name} - {clan.members} members")
```
