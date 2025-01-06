// // utils/logger.ts
// interface ErrorLogEntry {
//   timestamp: string;
//   endpointName: string;
//   requestId: string;
//   status?: number;
//   error?: string;
//   data?: any;
// }

// class Logger {
//   private isServer: boolean;
//   private readonly STORAGE_KEY = "rtk-query-errors";
//   private readonly MAX_LOGS = 1000;
//   private logFile: string;

//   constructor() {
//     this.isServer =
//       typeof process !== "undefined" &&
//       process.versions != null &&
//       process.versions.node != null;

//     if (this.isServer) {
//       const path = require("path");
//       console.log("############################################################")
//       console.log(__dirname)
//       console.log(path)
//       this.logFile = path.resolve(__dirname, "logs/rtk-query-errors.log");
//     } else {
//       this.logFile = "";
//     }
//   }

//   private formatLogMessage(error: ErrorLogEntry): string {
//     return `${JSON.stringify(error, null, 2)}\n${"=".repeat(80)}\n`;
//   }

//   public async logError(error: ErrorLogEntry): Promise<void> {
//     const logMessage = this.formatLogMessage(error);

//     try {
//       if (this.isServer) {
//         const fs = await import("fs/promises");
//         const path = await import("path");

//         const logDir = path.dirname(this.logFile);

//         // Ensure the directory and file exist
//         if (!(await fs.stat(logDir).catch(() => false))) {
//           await fs.mkdir(logDir, { recursive: true });
//         }

//         await fs.appendFile(this.logFile, logMessage);
//       } else {
//         const existingLogsJson = localStorage.getItem(this.STORAGE_KEY);
//         const existingLogs: string[] = existingLogsJson
//           ? JSON.parse(existingLogsJson)
//           : [];

//         existingLogs.push(logMessage);

//         while (existingLogs.length > this.MAX_LOGS) {
//           existingLogs.shift();
//         }

//         localStorage.setItem(this.STORAGE_KEY, JSON.stringify(existingLogs));
//       }

//       if (process.env.NODE_ENV === "development") {
//         console.error("RTK Query error:", error);
//       }
//     } catch (err) {
//       console.error("Failed to write error log:", err);
//       console.error("Original error:", error);
//     }
//   }

//   public async getLogs(): Promise<ErrorLogEntry[]> {
//     try {
//       if (this.isServer) {
//         const fs = await import("fs/promises");

//         const content = await fs.readFile(this.logFile, "utf-8");
//         return content
//           .split("=".repeat(80))
//           .filter((entry: string) => entry.trim())
//           .map((entry: string): ErrorLogEntry => JSON.parse(entry.trim()));
//       } else {
//         const logsJson = localStorage.getItem(this.STORAGE_KEY);
//         if (!logsJson) return [];
//         return JSON.parse(logsJson).map(
//           (log: string): ErrorLogEntry => JSON.parse(log)
//         );
//       }
//     } catch (err) {
//       console.error("Failed to retrieve logs:", err);
//       return [];
//     }
//   }

//   public async clearLogs(): Promise<void> {
//     try {
//       if (this.isServer) {
//         const fs = await import("fs/promises");
//         await fs.writeFile(this.logFile, "");
//       } else {
//         localStorage.removeItem(this.STORAGE_KEY);
//       }
//     } catch (err) {
//       console.error("Failed to clear logs:", err);
//     }
//   }
// }

// export const logger = new Logger();

// utils/logger.ts
interface ErrorLogEntry {
  timestamp: string;
  endpointName: string;
  requestId: string;
  status?: number;
  error?: string;
  data?: any;
}

class Logger {
  private logKey: string;

  constructor() {
    this.logKey = "errorLogs";
    this.setupGlobalErrorHandlers();
  }

  private saveLog(log: ErrorLogEntry): void {
    const logs = JSON.parse(
      localStorage.getItem(this.logKey) || "[]"
    ) as ErrorLogEntry[];
    logs.push(log);
    localStorage.setItem(this.logKey, JSON.stringify(logs));
  }

  public logError(error: ErrorLogEntry): void {
    const logMessage = this.formatLogMessage(error);
    console.error(logMessage); // Log to console for immediate feedback
    this.saveLog(error); // Save to local storage
  }

  private formatLogMessage(error: ErrorLogEntry): string {
    return `${JSON.stringify(error, null, 2)}\n${"=".repeat(80)}\n`;
  }

  private setupGlobalErrorHandlers(): void {
    window.onerror = (message, source, lineno, colno, error) => {
      const errorPayload = {
        timestamp: new Date().toISOString(),
        endpointName: "client-side",
        requestId: `${lineno}:${colno}`,
        error: `${message} at ${source}:${lineno}:${colno}`,
        data: error,
      };
      this.logError(errorPayload);
      return true;
    };

    window.addEventListener("unhandledrejection", (event) => {
      const errorPayload = {
        timestamp: new Date().toISOString(),
        endpointName: "client-side",
        requestId: "promise-rejection",
        error: event.reason,
      };
      this.logError(errorPayload);
    });
  }
}

const logger = new Logger();

export const logError = (error: ErrorLogEntry) => logger.logError(error);
