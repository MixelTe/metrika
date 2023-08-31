{
    post("/script/onopen", { eventId: "%eventId%" });

    const pushState = history.pushState;
    const replaceState = history.replaceState;

    history.pushState = function ()
    {
        pushState.call(history, ...arguments);
        onPageChange();
    };
    history.replaceState = function ()
    {
        replaceState.call(history, ...arguments);
        onPageChange();
    };
    window.addEventListener('popstate', function ()
    {
        window.dispatchEvent(new Event('locationchange'))
        onPageChange();
    });

    function onPageChange()
    {
        post("/script/event", {
            event: "page",
        });
    }

    function post(path, content)
    {
        const url = "%url%";
        const appCode = "%appCode%";
        fetch(url + path, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                ...content,
                appCode,
                fromTag: new URL(location.href).searchParams.get("from") || "",
                page: trimEnd(new URL(location.href).pathname, "/") || "/",
            }),
        })
    }

    function trimEnd(str, ch = " ")
    {
        for (let i = str.length - 1; i >= 0; i--)
        {
            if (str[i] != ch)
            {
                return str.slice(0, i + 1)
            }
        }
        return ""
    }
}