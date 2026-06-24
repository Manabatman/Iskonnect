/**
 * IndexedDB cache for last scholarship search results (offline resilience on 3G/4G drops).
 */

const DB_NAME = "iskonnect-offline";
const STORE = "search-cache";
const DB_VERSION = 1;

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onerror = () => reject(req.error);
    req.onsuccess = () => resolve(req.result);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE);
      }
    };
  });
}

/** Persist the latest search payload under a stable key. */
export async function cacheSearchResults(key: string, payload: unknown): Promise<void> {
  try {
    const db = await openDb();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, "readwrite");
      tx.objectStore(STORE).put({ savedAt: Date.now(), payload }, key);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    db.close();
  } catch {
    /* IndexedDB unavailable — non-fatal */
  }
}

/** Read cached search results; returns null when missing or expired. */
export async function readCachedSearchResults<T>(
  key: string,
  maxAgeMs = 1000 * 60 * 60 * 24,
): Promise<T | null> {
  try {
    const db = await openDb();
    const record = await new Promise<{ savedAt: number; payload: T } | undefined>((resolve, reject) => {
      const tx = db.transaction(STORE, "readonly");
      const req = tx.objectStore(STORE).get(key);
      req.onsuccess = () => resolve(req.result as { savedAt: number; payload: T } | undefined);
      req.onerror = () => reject(req.error);
    });
    db.close();
    if (!record) return null;
    if (Date.now() - record.savedAt > maxAgeMs) return null;
    return record.payload;
  } catch {
    return null;
  }
}
