import uuid
import json
from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import Group, Document

def index(request, group_name=None):
    # Generate a UUID if no group_name is provided
    if group_name is None:
        group_name = str(uuid.uuid4())
        return redirect('index', group_name=group_name)

    group = Group.objects.filter(name=group_name).first()
    cache_key = f'document_cache_{group_name}'  # Cache key specific to the group name
    docs_json = "{}"  # Initialize as an empty JSON string

    if group:
        # Check if the document is cached
        cached_doc = cache.get(cache_key)

        if cached_doc:
            docs_json = cached_doc  # Use cached content if available
            print("cache working successfully......")
        else:
            # Fetch the latest document from the database
            docs = Document.objects.filter(group=group).last()
            if docs:
                doc_dict = {
                    "group": {
                        "id": docs.group.id,
                        "name": docs.group.name,
                    },
                    "content": docs.content,  # Assuming 'content' is a field in your Document model
                    "timestamp": docs.updated_at.isoformat() if docs.updated_at else None,
                }
                docs_json = json.dumps(doc_dict)
                cache.set(cache_key, docs_json)  # Cache the document for future requests
    else:
        # Create a new group if it doesn't exist
        group = Group(name=group_name)
        group.save()

    return render(request, 'documents/index.html', {'group_name': group_name, 'docs_json': docs_json})

# Function to save the document only if the content has changed and update the cache
def save_document(group_name, new_content):
    group = Group.objects.filter(name=group_name).first()
    cache_key = f'document_cache_{group_name}'

    if group:
        docs = Document.objects.filter(group=group).last()
        if docs and docs.content != new_content:
            docs.content = new_content
            docs.save()

            # Update cache after saving the document
            doc_dict = {
                "group": {
                    "id": docs.group.id,
                    "name": docs.group.name,
                },
                "content": docs.content,
                "timestamp": docs.updated_at.isoformat() if docs.updated_at else None,
            }
            docs_json = json.dumps(doc_dict)
            cache.set(cache_key, docs_json, timeout=3600)  # Cache the updated document
