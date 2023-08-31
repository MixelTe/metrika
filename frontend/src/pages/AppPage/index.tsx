import { useParams } from "react-router-dom";
import styles from "./styles.module.css"
import Layout from "../../components/Layout";
import { useApp } from "../../api/app";
import Spinner from "../../components/Spinner";
import { useStats, Stats, StatsParams, useStatsVisitors } from "../../api/stats";
import Chart, { ChartData, ChartItem } from "../../components/Chart";
import { useState } from "react";
import { UseQueryResult } from "react-query";
import { dateToInptValue, datetimeToString } from "../../utils/dates";
import { useTitle } from "../../utils/useTtile";

export default function AppPage()
{
	const [startDate, setStartDate] = useState(() =>
	{
		const date = new Date();
		date.setHours(0, 0, 0, 0);
		date.setDate(date.getDate() - 1);
		return date;
	});
	const [endDate, setEndDate] = useState(() =>
	{
		const date = new Date();
		date.setHours(0, 0, 0, 0);
		return date;
	});
	const [group, setGroup] = useState<StatsParams["group"]>("hour");

	const appId = useParams()["appId"]!;
	const app = useApp(appId);
	useTitle([app.data?.name || "App"]);
	const statsParams = { group, type: "requests", start: startDate, end: (() => { const date = new Date(endDate); date.setDate(date.getDate() + 1); return date })() } as StatsParams;
	const stats_requests = useStats(appId, { ...statsParams, type: "requests" });
	const stats_visitors = useStats(appId, { ...statsParams, type: "visitors" });
	const stats_visitorsNew = useStats(appId, { ...statsParams, type: "visitors", newVisitors: true });
	const stats_fromTag = useStats(appId, { ...statsParams, type: "fromTag" });
	const visitors = useStatsVisitors(appId, statsParams);
	const visitorsNew = useStatsVisitors(appId, { ...statsParams, newVisitors: true });

	function processChartData(queryResult: UseQueryResult<Stats[], unknown>, avarege = true)
	{
		const data = queryResult.data
		return data?.map(v =>
		{
			const data = v.values;
			const _startDate = new Date(startDate);
			const _endDate = new Date(endDate);
			_startDate.setHours(0);
			_endDate.setHours(24);
			const now = new Date();
			now.setMinutes(Math.floor(now.getMinutes() / 10 + 1) * 10, 0, 0);
			let date = +_startDate;
			let end = +(_endDate < now ? _endDate : now);
			const dateAdd = {
				minute: 1000 * 60 * 10,
				hour: 1000 * 60 * 60,
				day: 1000 * 60 * 60 * 24,
			}[group];
			return {
				label: v.label,
				avarege: avarege,
				values: (data?.map(v => ({ value: v.count, label: v.date })) || []).reduce((r, v, i) =>
				{
					const vdate = new Date(v.label);
					v.label = datetimeToString(vdate);
					const vdaten = +vdate;

					while (vdaten > date)
					{
						r.push({ value: 0, label: datetimeToString(new Date(date)) });
						date += dateAdd;
					}
					date += dateAdd;
					r.push(v);
					while (i + 1 == data?.length && date < end)
					{
						r.push({ value: 0, label: datetimeToString(new Date(date)) });
						date += dateAdd;
					}

					return r;
				}, [] as ChartItem[])
			} as ChartData;
		}) || [];
	}

	return (
		<Layout centeredPage gap="1em" backLink="/">
			{(app.isLoading || stats_requests.isLoading || stats_visitors.isLoading || stats_fromTag.isLoading) && <Spinner />}
			{app.isError && `app: ${app.error}`}
			{stats_requests.isError && `stats_requests: ${stats_requests.error}`}
			{stats_visitors.isError && `stats_visitors: ${stats_visitors.error}`}
			{stats_fromTag.isError && `stats_visits: ${stats_fromTag.error}`}
			{visitors.isError && `visitors: ${visitors.error}`}
			<h1>{app.data?.name}</h1>
			<div>
				<span>Period: </span>
				<label>
					<span>Start: </span>
					<input type="date" value={dateToInptValue(startDate)} onChange={e => setStartDate(v => e.target.valueAsDate || v)} />
				</label>
				<label>
					<span>End: </span>
					<input type="date" value={dateToInptValue(endDate)} onChange={e => setEndDate(v => e.target.valueAsDate || v)} />
				</label>
				<label>
					<span>Group: </span>
					<select value={group} onChange={e => setGroup(e.target.value as any)}>
						<option value="minute">10 Minutes</option>
						<option value="hour">Hour</option>
						<option value="day">Day</option>
					</select>
				</label>
			</div>
			<div className={styles.charts}>
				<Chart title="Requests" data={processChartData(stats_requests)} />
				<Chart title="Visitors" valuesSum={visitors.data} data={processChartData(stats_visitors)} />
				<Chart title="New visitors" valuesSum={visitorsNew.data} data={processChartData(stats_visitorsNew)} />
				<Chart title="From tag" data={processChartData(stats_fromTag, false)} />
			</div>
		</Layout>
	);
}
