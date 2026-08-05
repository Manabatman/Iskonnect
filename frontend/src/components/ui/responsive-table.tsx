import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export interface ResponsiveTableColumn<T> {
  key: string;
  header: string;
  cell: (row: T) => React.ReactNode;
  /** Shown as label in mobile card layout */
  mobileLabel?: string;
}

interface ResponsiveTableProps<T> {
  columns: ResponsiveTableColumn<T>[];
  data: T[];
  rowKey: (row: T) => string;
  emptyMessage?: string;
  className?: string;
}

/** MOB-11 — table on md+, stacked cards on mobile. */
export function ResponsiveTable<T>({
  columns,
  data,
  rowKey,
  emptyMessage = "No rows to display.",
  className,
}: ResponsiveTableProps<T>) {
  if (data.length === 0) {
    return <p className="text-sm text-muted-foreground">{emptyMessage}</p>;
  }

  return (
    <div className={className}>
      <div className="hidden md:block">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((col) => (
                <TableHead key={col.key}>{col.header}</TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((row) => (
              <TableRow key={rowKey(row)}>
                {columns.map((col) => (
                  <TableCell key={col.key}>{col.cell(row)}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="space-y-3 md:hidden">
        {data.map((row) => (
          <Card key={rowKey(row)}>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">{columns[0]?.cell(row)}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              {columns.slice(1).map((col) => (
                <div key={col.key} className="flex justify-between gap-4">
                  <span className="text-muted-foreground">{col.mobileLabel ?? col.header}</span>
                  <span className="text-right font-medium">{col.cell(row)}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
