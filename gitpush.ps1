param (
    [string]$Message = "Update"
)

git add .
git commit -m "$Message"
git push origin main
