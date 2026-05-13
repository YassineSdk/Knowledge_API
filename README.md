# Knowledge_API


# knowledge consolidation : 

``` python
for layer in layers:

    prompt = build_prompt(
        layer_config,
        chunks
    )

    response = llm(prompt)

    parsed_layer = json.loads(response)

    dossier[layer] = parsed_layer

# layer storage structure : 
{
    "layer": str,
    "summary": str,
    "articles": [

        {
            "article_id": str,
            "title": str,
            "content": str,
            "citations": list[str]
        },
        .....
        ,
        {
            "article_id": str,
            "title": str,
            "content": str,
            "citations": list[str]
        }

    ]
}

```

