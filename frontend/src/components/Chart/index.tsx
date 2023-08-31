import { useState } from "react";
import styles from "./styles.module.css"

export default function Chart({ data, title, valuesSum }: ChartProps)
{
	const [cursor, setCursor] = useState(-1);
	const empty = data.length == 0;
	data.forEach(v =>
	{
		if (v.values.length == 1) v.values = [v.values[0], v.values[0]];
	});
	const maxV = data.reduce((p, v) => Math.max(p, v.values.reduce((p, v) => Math.max(p, v.value), 0)), 0);
	const width = 300;
	const height = 100;
	const padding = 10;
	const colors = [
		{ fill: "rgba(139, 255, 84, 0.2)", stroke: "rgb(139, 197, 84)" },
		{ fill: "rgba(253, 204, 53, 0.2)", stroke: "rgb(253, 204, 53)" },
		{ fill: "rgba(253, 90, 62, 0.2)", stroke: "rgb(253, 90, 62)" },
		{ fill: "rgba(119, 182, 231, 0.2)", stroke: "rgb(119, 182, 231)" },
		{ fill: "rgba(169, 85, 184, 0.2)", stroke: "rgb(169, 85, 184)" },

		{ fill: "rgba(92, 170, 56, 0.2)", stroke: "rgb(92, 170, 56)" },
		{ fill: "rgba(168, 136, 35, 0.2)", stroke: "rgb(168, 136, 35)" },
		{ fill: "rgba(168, 60, 41, 0.2)", stroke: "rgb(168, 60, 41)" },
		{ fill: "rgba(79, 121, 154, 0.2)", stroke: "rgb(79, 121, 154)" },
		{ fill: "rgba(112, 56, 122, 0.2)", stroke: "rgb(112, 56, 122)" },
	]
	const dataLength = data[0]?.values?.length || 0;
	const step = width / (dataLength - 1);
	const indexToX = (i: number) => Math.round(i * step + padding);
	const dataToPoint = (v: number, i: number) => ({
		x: indexToX(i),
		x1: indexToX(Math.max(i - 0.5, 0)),
		x2: indexToX(Math.min(i + 0.5, dataLength - 1)),
		y: Math.round((1 - v / maxV) * height + padding)
	})
	const lineTop = { y: dataToPoint(maxV, 0).y, label: maxV };
	const lineHalfV = maxV == 1 ? 0.5 : Math.floor(maxV / 2);
	const lineHalf = { y: dataToPoint(lineHalfV, 0).y, label: lineHalfV };
	return <div className={styles.root}>
		<h3>{title}</h3>
		<svg
			width={width + padding * 2}
			height={height + padding * 2}
			onMouseMove={e =>
			{
				const x = e.nativeEvent.offsetX - padding;
				setCursor(Math.min(Math.max(Math.round(x / step), 0), dataLength - 1));
			}}
			onMouseLeave={() => setCursor(-1)}
		>
			{empty ? <>
				<text x={width / 2} y={height / 2}>No data</text>
			</> : <>
				<line x1={0} x2={width + padding * 2} y1={lineTop.y} y2={lineTop.y} strokeWidth={1} stroke="#00000040" />
				<text x={2} y={lineTop.y + 12} fontSize={12} >{lineTop.label}</text>
				<line x1={0} x2={width + padding * 2} y1={lineHalf.y} y2={lineHalf.y} strokeWidth={1} stroke="#00000040" />
				<text x={2} y={lineHalf.y + 12} fontSize={12} >{lineHalf.label}</text>
				{data.map((v, i) =>
				{
					const points = v.values.map((v, i) => dataToPoint(v.value, i));
					const color = colors[i] || colors[0];
					return <path
						fill={color.fill}
						stroke={color.stroke}
						strokeWidth={2}
						// d={`M${points.map(p => `${p.x},${p.y}`).join(" L")} L${width + padding},${height + padding * 2} L${padding},${height + padding * 2} L${points[0].x},${points[0].y}`}
						d={`M${points.map(p => `${p.x1},${p.y}L${p.x2},${p.y}`).join(" L")} L${width + padding},${height + padding * 2} L${padding},${height + padding * 2} L${points[0].x},${points[0].y}`}
					/>
				})}

				{/* {points.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={2} fill="#0000ff" />)} */}
				{cursor >= 0 && <line x1={cursor * step + padding} x2={cursor * step + padding} y1={0} y2={height + padding * 2} strokeWidth={1} stroke="gray" />}
			</>}
		</svg>
		{data.map(v =>
		{
			const sum = v.values.reduce((p, v) => p + v.value, 0);
			return <div className={styles.desc}>
				<div>{v.label}</div>
				<div>{cursor < 0 ? v.avarege && (Math.round(sum / dataLength * 10) / 10 || 0) : v.values[cursor]?.label}</div>
				<div>{cursor < 0 ? valuesSum || sum || 0 : v.values[cursor]?.value}</div>
			</div>
		})}
	</div>
}

interface ChartProps
{
	data: ChartData[],
	title?: string,
	valuesSum?: number,
}

export interface ChartData
{
	label: string,
	values: ChartItem[],
	avarege: boolean,
}
export interface ChartItem
{
	value: number,
	label: string,
}

