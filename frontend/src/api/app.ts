import { useMutation, useQuery, useQueryClient } from "react-query";
import { ResponseMsg } from "./dataTypes";
import fetchPost from "../utils/fetchPost";

export default function useApps()
{
	return useQuery("apps", getApps);
}
export function useMutationNewApp()
{
	const queryClient = useQueryClient();
	const mutation = useMutation({
		mutationFn: postNewApp,
		onSuccess: (data) =>
		{
			if (queryClient.getQueryState("apps")?.status == "success")
				queryClient.setQueryData("apps", (apps?: App[]) => apps ? [...apps, data] : [data]);
		},
	});
	return mutation;
}

export interface App
{
    id: number,
    code: string,
    name: string,
}

export interface NewAppData
{
    name: string,
}

async function getApps(): Promise<App[]>
{
	const res = await fetch("/api/apps");
	const data = await res.json();
	if (!res.ok) throw (data as ResponseMsg).msg;

	return data as App[];
}

async function postNewApp(appData: NewAppData)
{
	const res = await fetchPost("/api/app", appData);
	const data = await res.json();
	if (!res.ok) throw (data as ResponseMsg).msg;
	return data as App;
}
