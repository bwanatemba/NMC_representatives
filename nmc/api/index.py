from nmc.wsgi import application

# Resolve Vercel expects 'app' or 'handler' issue
app = application
