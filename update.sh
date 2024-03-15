# get the latest code from main branch (should be stable)
echo "Getting the latest changes from main branch"
git fetch
git checkout main
git pull

# delete the old venv
echo "Removing old venv"
deactivate
rm -rf .venv/

# recreate venv
source venv.sh
