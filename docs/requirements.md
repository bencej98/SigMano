# SigMano Requirements

## Server Requirements

## Client Requirements

## Database Requirements

- If there is no database behind the server, the server should create one upon the first launch.
- Players should be authenticated using the database.
- Each player should be able to register via the client. The username and password should be stored in the database.
- The database shall store each player's wins, losses, kills, and deaths.

## Interface Requirements
- The client and the server should communicate with each other using JSON format.
- The structure of the JSON message shall depend on the type of action that the user performs.

### Client-Server communication

- The JSON convention should be as follows during client-server communication:
```json
{
	"Type": "Action",
	"Payload": {
		"1": "hit",
		"2": "defend"
	}
}
```
```json
{
	"Type": "Registration",
	"Payload": {
		"username": "xy",
		"password": "xy"
	}
}
```
```json
{
	"Type": "Closed",
	"Payload": {}
}
```
```json
{
	"Type": "Auth","Payload": {"username": "xy","password": "xy"}
}
```


### Server-Client communicaton
- The JSON convention should be as follows during client-server communication:
```json
{
	"Type": "Position",
	"Payload": {
		"User": [x, y]
	}
}
```
```json
{
	"Type": "Event",
	"Payload": {
		"happening": "msg",
		"outcome": "msg"
	}
}
```

```json
{
	"Type": "Auth","Payload": true // false
}
```