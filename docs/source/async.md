# Async Usage

The library provides a fully async client under `clash_royale.aio`. It mirrors the synchronous API but uses `async`/`await`, making it suitable for asyncio-based applications.

## Getting Started

```python
from clash_royale.aio import Client

async with Client(api_key="your-api-key") as client:
    player = await client.players.get("#9G9JL8QU")
    print(player.name)
```

The async client **must** be used as an async context manager (or closed manually with `await client.aclose()`). This ensures the underlying HTTP connection pool is properly cleaned up.

### Using a proxy

Proxy usage works the same as the sync client:

```python
from clash_royale.aio import Client

async with Client(
    api_key="your-api-key",
    proxy="https://proxy.royaleapi.dev",
) as client:
    ...
```

## Resources

All resource methods that perform a single API call are `async`:

```python
# Single-item endpoints are async
player = await client.players.get("#9G9JL8QU")
clan = await client.clans.get("#2Q8CCP0")
tournament = await client.tournaments.get("#2PP")

# Battlelog and upcoming chests are also async
battles = await client.players.get_battlelog("#9G9JL8QU")
chests = await client.players.get_upcoming_chests("#9G9JL8QU")
```

Methods that return a {class}`PaginatedList <clash_royale.aio.PaginatedList>` are **not** async themselves (they return immediately), but the list fetches pages asynchronously when you access its items:

```python
# Returns a PaginatedList immediately (no await)
results = client.clans.search(name="Legend", limit=10)
members = client.clans.get_members("#2Q8CCP0", limit=20)
cards = client.cards.list(limit=10)
```

## Async Pagination

The async {class}`PaginatedList <clash_royale.aio.PaginatedList>` provides explicit async methods instead of magic methods like `__getitem__`.

### Async iteration

```python
results = client.clans.search(name="Legend", limit=20)

async for clan in results:
    print(clan.name)
```

### Fetching all items

```{warning}
`all()` fetches **every page** from the API, which may result in many requests
and large memory usage. Always set a `limit` when creating the paginated list,
or prefer async iteration with an early `break`.
```

```python
# Safe: limit is set
results = client.clans.search(name="Legend", limit=20)
clans = await results.all()
print(len(clans))  # At most 20
```

### Index access

```python
results = client.leaderboards.get(leaderboard_id, limit=100)

first = await results.get(0)
fifth = await results.get(4)
```

Negative indexing is not supported — use `all()` and index the resulting list instead.

### Slicing

```python
top_10 = await results.slice(0, 10)
next_10 = await results.slice(10, 20)
```

### First item

```python
first = await results.first()  # Returns None if empty
```

### `limit` and `page_size`

These work identically to the sync client:

```python
# Fetch at most 50 players, 25 per API request
players = client.leaderboards.get(leaderboard_id, limit=50, page_size=25)

async for player in players:
    print(player.name)
```

## Comparison with Sync Client

| Operation | Sync | Async |
|-----------|------|-------|
| Get a resource | `client.players.get(tag)` | `await client.players.get(tag)` |
| Context manager | `with client:` | `async with client:` |
| Iterate | `for item in results:` | `async for item in results:` |
| Get all items | `list(results)` | `await results.all()` |
| Index access | `results[0]` | `await results.get(0)` |
| Slice | `results[:10]` | `await results.slice(0, 10)` |
| First item | `next(results)` | `await results.first()` |

Models, exceptions, and types are shared between the sync and async clients. You import them from the top-level `clash_royale` package:

```python
from clash_royale.aio import Client
from clash_royale import ClashRoyaleNotFoundError, Player
```

## Error Handling

Error handling is the same as the sync client, using the same exception classes:

```python
import clash_royale
from clash_royale.aio import Client

async with Client(api_key="your-api-key") as client:
    try:
        player = await client.players.get("#INVALID")
    except clash_royale.ClashRoyaleNotFoundError:
        print("Player not found")
    except clash_royale.ClashRoyaleHTTPError as e:
        print(f"API error: {e}")
```

## Complete Example

```python
import asyncio

from clash_royale.aio import Client


async def main():
    async with Client(api_key="your_api_key") as client:
        # Get a player
        player = await client.players.get("#9G9JL8QU")
        print(f"{player.name} - {player.trophies} trophies")

        # Search clans
        results = client.clans.search(name="Legend", min_members=40, limit=10)
        async for clan in results:
            print(f"{clan.name} - {clan.members} members")

        # Get top leaderboard players
        players = client.leaderboards.get(170000008, limit=10, page_size=10)
        top_10 = await players.all()
        for p in top_10:
            print(f"{p.rank}. {p.name} - {p.score} points")


asyncio.run(main())
```
