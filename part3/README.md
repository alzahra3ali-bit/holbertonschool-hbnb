# HBnB - Part 3: Authentication & Database Persistence

Part 3 of the Holberton HBnB project. It builds on the Part 2 API by adding
JWT authentication, role-based access control, and persistent storage via SQLAlchemy.


## Project structure

```
part3/
├── app/
│   ├── api/v1/          # Route handlers: users, amenities, places, reviews, auth
│   ├── models/          # SQLAlchemy models: User, Place, Review, Amenity, BaseModel
│   ├── persistence/     # Repository layer 
│   └── services/        
├── tests/               
├── SQL script/          # hbnb.sql — schema/initial data
├── er_diagram.md        # Entity relationship diagram
├── config.py            # App configuration (DB URI, secret key, debug flag)
├── run.py               
└── requirements.txt
```

## Data model

See [er_diagram.md](er_diagram.md) for the full er diagram.

