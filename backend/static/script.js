{
    const eventId = "%eventId%";
    const url = "%url%";
    fetch(url + "/script/onopen", {
        method: "POST",
		headers: {
			"Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
            eventId,
            fromTag: new URL(location.href).searchParams.get("from") || "",
        }),
    })
}