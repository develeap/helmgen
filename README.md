# helmgen
## helm generator for service kubernetes
### Packaging from source
1. Clone the repo:
```bash
git clone git@github.com:develeap/helmgen.git
```
2. Start by installing pipenv:
```bash
install pipenv -- pip install pipenv
```
3. Package the app using click setup:
```bash
cd helmgen/app && \
pipenv install && \
python setup.py install
```
4. Run the app using cli:
```bash
helmgen apply
```
## running as docker container
```bash
docker run -it --rm -v ~/.kube/config:~/.kube/config -w /app appgen bash -c “helmgen apply”
```
