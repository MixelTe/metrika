import { useQuery } from "react-query";
import { ResponseMsg } from "./dataTypes";
import { datetimeToISO } from "../utils/dates";

export function useStats(appId: number | string, params: StatsParams)
{
	return useQuery(["stats", `${appId}`, params], () => getStats(appId, params));
}

export function useStatsVisitors(appId: number | string, params: VisitorsParams)
{
	return useQuery(["statsVisitors", `${appId}`, params], () => getVisitors(appId, params));
}

export interface Stats
{
	label: string,
	values: StatsItem[],
}

export interface StatsItem
{
	count: number,
	date: string,
}

export interface StatsParams
{
	group: "minute" | "hour" | "day",
	type: "visitors" | "visits" | "requests" | "fromTag",
	start: Date,
	end: Date,
	newVisitors: boolean,
}

export interface VisitorsParams
{
	start: Date,
	end: Date,
	newVisitors: boolean,
}

async function getStats(appId: number | string, params: StatsParams): Promise<Stats[]>
{
	const res = await fetch("/api/stats/" + appId +
		`?group=${params.group}&type=${params.type}&start=${datetimeToISO(params.start)}&end=${datetimeToISO(params.end)}&new=${params.newVisitors ? 1 : 0}`);
	const data = await res.json();
	if (!res.ok) throw (data as ResponseMsg).msg;

	return data as Stats[];
}

async function getVisitors(appId: number | string, params: VisitorsParams): Promise<number>
{
	const res = await fetch("/api/stats/visitors/" + appId + `?start=${datetimeToISO(params.start)}&end=${datetimeToISO(params.end)}&new=${params.newVisitors ? 1 : 0}`);
	const data = await res.json();
	if (!res.ok) throw (data as ResponseMsg).msg;

	return data as number;
}
