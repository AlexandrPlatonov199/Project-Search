"""Repositories should be dumb, while services, on the contrary, should be
smart. That's why :class:`.Repository` must contain a minimum set of.

**C.R.U.D.** methods.

- **C** - Create
- **R** - Read
- **U** - Update
- **D** - Delete

Note:
    The repository must contain a minimum set of instructions for interacting with the
    target database.
"""