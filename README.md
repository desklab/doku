# doku

From the German word **Dokument** (document).

## Development

**doku** overwrites **Flask's** default command line interface using **click**.
The cli can be accessed using the file `manage.py` (alluding to **django's** `manage.py`):

```bash
# Note that you might want to set FLASK_DEBUG and FLASK_ENV first:
$ export FLASK_DEBUG=1
$ export FLASK_ENV=development

$ python manage.py run
```

To create a user, the `create-user` command is available.

### Static Files and JavaScript

The front-end is developed mainly in [**vue.js**](https://vuejs.org/). It can be found inside the `/doku/static` directory.
To build these static files, you need **Node.js** and **npm**:

```bash
# These commands need to be run inside the /doku/static directory
# use "cd doku/static" to navigate there

$ npm install

# Build files for production
$ npm run build

# Development server
$ npm run dev
```

Our CSS framework of choice is [**SPECTRE.CSS**](https://picturepan2.github.io/spectre/).
Additional styles can be found in the `/doku/static/src` directory.

### Migrations

**doku** uses [`alembic`](https://alembic.sqlalchemy.org/) for migrations. Those can be found inside the
`/alembic` directory.  
These commands are especially useful:

```bash
$ alembic revision --autogenerate -m "migration_name"
$ alembic upgrade head

# Also useful for marking migrations as current:
$ alembic stamp head
```

For more information you might want to take a look at the [**basic_flask** project
by davidism on GitHub](https://github.com/davidism/basic_flask).

Additionally, **doku** implements a method that will call **Flask_SQAlchemy's** `create_all`:

```bash
$ python manage.py init-db
```

### Contribute

Pull requests are always welcome! Feel free to fork the project and improve it.

## License

This project is licensed under the **BSD 3-Clause "New" or "Revised" License**:

    Copyright (c) 2020 Jonas Drotleff. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
