# Usage

## First Steps

To start calling the API, you first need to instantiate a `Client` with your API key:

```python
client = clash_royale.Client(api_key='your-api-key')
```

While this usage is simple and convenient for using in the Python console, it's best to use it as a context manager:

```python
with clash_royale.Client(api_key='your-api-key') as client:
    ...
```

This is [the recommended way to use it by httpx](https://www.python-httpx.org/advanced/clients/#usage), which is the library we use under the hood.

From there, you can search for clans:

```python
client.clans.search('Legend')
```

```
<PaginatedList [
 <ClanSearchResult: Legend>,
 <ClanSearchResult: Legend Squad>,
 <ClanSearchResult: The Legend>,
 <ClanSearchResult: Legends>,
 <ClanSearchResult: Legend Empire>,
 '...']>
```

The above returned a lot of clans, wrapped in a `PaginatedList`, which is a list-like object (see the dedicated page about pagination for more details).

You can also get information about a specific player by their tag:

```python
client.players.get('#9G9JL8QU')
```

```
<Player: PlayerName>
```

## Main Concepts

As we have just seen above, the entry point is the `Client` class, which gives access to various resource endpoints. The methods are attempting to map to the REST API endpoints from Clash Royale.

You may have noticed from the above examples, but depending on the endpoint that is being called, the methods will return various types of resources. All the resources are listed in the resources reference page.

## More Examples

### Getting Fields About a Resource

When you get a resource, you have access to all the fields that are in the REST API response. For example, all the fields presented in the documentation for the player object are accessible as attributes on the `Player` resource:

```python
>>> player = client.players.get('#9G9JL8QU')

>>> player.name
'PlayerName'

>>> player.trophies
5432

>>> player.level
14

>>> player.wins
1234
```

### Getting Related Resources

As well as giving access to its own attributes, resources provide methods to fetch related data.

For example, when you get a player, you can get their battle log or upcoming chests. From a clan, you can get its members or river race log:

```python
# Get a clan
>>> clan = client.clans.get('#2Q8CCP0')

>>> clan.name
'ClanName'

>>> clan.members
47

# Get clan members
>>> members = client.clans.get_members('#2Q8CCP0')
>>> members[:3]
[<ClanMember: Member1>,
 <ClanMember: Member2>,
 <ClanMember: Member3>]

# Get player's battle log
>>> player = client.players.get('#9G9JL8QU')
>>> battlelog = client.players.get_battlelog('#9G9JL8QU')
>>> battlelog[:3]
[<Battle: ...>,
 <Battle: ...>,
 <Battle: ...>]
```

### Working with Leaderboards

You can fetch leaderboard data with pagination control:

```python
# Get available leaderboards
>>> leaderboards = client.leaderboards.list()
>>> leaderboards[0]
<Leaderboard: Players>

# Get top players from a leaderboard
>>> players = client.leaderboards.get(leaderboard_id=57000000, limit=10)
... for player in players:
...    print(f"{player.rank}. {player.name} - {player.trophies}")
```

### Searching with Filters

When searching for clans or tournaments, you can use filters:

```python
# Search clans with filters
clans = client.clans.search(
    name='Legend',
    min_members=40,
    location_id=57000249,  # United States
    limit=20
)

for clan in clans:
    print(f"{clan.name} - {clan.members} members")
```

## Getting the Raw Data

At some point, you might want to get the resources exported as Python dictionaries to store them somewhere else or transform them further.

Each resource has a `model_dump()` method to export its content as a dictionary:

```python
>>> player = client.players.get('#9G9JL8QU')
>>> player.model_dump()
{'tag': '#9G9JL8QU',
 'name': 'PlayerName',
 'level': 14,
 'trophies': 5432,
 'best_trophies': 6123,
 'wins': 1234,
 'losses': 987,
 ...}
```

You can also use `model_dump_json()` to get a JSON string directly:

```python
>>> player.model_dump_json()
'{"tag":"#9G9JL8QU","name":"PlayerName",...}'
```

## Authentication

The Clash Royale API requires an API key for all requests. You can get an API key by:

1. Creating an account at [https://developer.clashroyale.com](https://developer.clashroyale.com)
2. Creating an API key with your IP address whitelisted

Once you have your API key, pass it to the `Client`:

```python
client = clash_royale.Client(api_key='your-api-key')
```

**Important:** Keep your API key secret! Don't commit it to version control. Consider using environment variables:

```python
import os
client = clash_royale.Client(api_key=os.environ['CLASH_ROYALE_API_KEY'])
```

### Using a proxy

If your server does not have a static IP address, you can use a proxy server.

For exemple you can use the proxy solution provided by the [RoyaleAPI team](https://royaleapi.com/) by setting the `proxy` parameter to `https://proxy.royaleapi.dev`.

```python

>>> client = clash_royale.Client(
        api_key="your_api_key_here",
        proxy="https://proxy.royaleapi.dev",
    )
```
For more detail about RoyaleAPI proxy usage, check their [documentation](https://docs.royaleapi.com/proxy.html).

If you want to host your own proxy server, there is a nuxt web app you can use available at [https://github.com/AndreVarandas/royale-proxy-api](https://github.com/AndreVarandas/royale-proxy-api). Made by  [@AndreVarandas](https://github.com/AndreVarandas/)

## Error Handling

The client will raise specific exceptions for different error scenarios:

```python
import clash_royale

try:
    player = client.players.get('#INVALID')
except clash_royale.ClashRoyaleNotFoundError:
    print("Player not found")
except clash_royale.UnauthorizedError:
    print("Invalid API key")
except clash_royale.RateLimitError:
    print("Rate limit exceeded")
except clash_royale.ClashRoyaleHTTPError as e:
    print(f"API error: {e}")
```
