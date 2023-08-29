import { useState } from "react";
import styles from "./styles.module.css"

export default function Chart({ data, title, valuesSum }: ChartProps)
{
	const [cursor, setCursor] = useState(-1);
	const empty = data.length == 0;
	if (data.length == 1) data = [data[0], data[0]];
	const maxV = data.reduce((p, v) => p > v.value ? p : v.value, 0);
	const width = 300;
	const height = 100;
	const padding = 10;
	const step = width / (data.length - 1);
	const dataToPoint = (v: number, i: number) => ({ x: Math.round(i * step + padding), y: Math.round((1 - v / maxV) * height + padding) })
	const points = data.map((v, i) => dataToPoint(v.value, i));
	const sum = data.reduce((p, v) => p + v.value, 0);
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
				setCursor(Math.min(Math.max(Math.round(x / step), 0), data.length - 1));
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
				<path
					fill="rgba(139, 255, 84, 0.2)"
					stroke="rgb(139, 197, 84)"
					strokeWidth={2}
					d={`M${points.map(p => `${p.x},${p.y}`).join(" L")} L${width + padding},${height + padding * 2} L${padding},${height + padding * 2} L${points[0].x},${points[0].y}`}
				/>
				{/* {points.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={2} fill="#0000ff" />)} */}
				{cursor >= 0 && <line x1={cursor * step + padding} x2={cursor * step + padding} y1={0} y2={height + padding * 2} strokeWidth={1} stroke="gray" />}
			</>}
		</svg>
		<div className={styles.hov}>{cursor >= 0 && <>
			<span>{data[cursor]?.label}</span>
			<span>{data[cursor]?.value}</span>
		</>}</div>
		<div className={styles.desc}>
			<span>Sum:</span>
			<span>{valuesSum || sum || 0}</span>
		</div>
		<div className={styles.desc}>
			<span>Avarage:</span>
			<span>{Math.round(sum / data.length * 10) / 10 || 0}</span>
		</div>
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
	value: number,
	label: string,
}

