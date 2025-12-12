"use client";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

export function ScoreTrend({ data }: { data: { date: string; gpt4: number; gemini: number }[] }) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="gpt4" stroke="#2F8EFF" />
          <Line type="monotone" dataKey="gemini" stroke="#10B981" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
