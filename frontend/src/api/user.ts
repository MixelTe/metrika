import { useQuery } from "react-query";
import { ResponseMsg } from "./dataTypes";

export default function useUser()
{
	return useQuery("user", getUser);
}

export interface User
{
	auth: boolean,
	id: number,
	name: string,
	login: string,
	operations: string[],
}

async function getUser(): Promise<User>
{
	const res = await fetch("/api/user");
	const data = await res.json();

	if (res.status == 401) return { auth: false, id: -1, login: "", name: "", operations: [] };
	if (!res.ok) throw (data as ResponseMsg).msg;

	const user = data as User;
	user.auth = true;
	return user;
}
