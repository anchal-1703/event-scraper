"use client";
import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { motion } from "motion/react";

export function EventModal({ open, setOpen, eventData, setEventData }) {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    setError("");
  };

  const handleSubmit = async () => {
    if (!email || !email.includes("@")) {
      setError("Please enter a valid email address");
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      const response = await fetch("http://localhost:5000/api/email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (data.success) {
        setSuccess(true);

        // Redirect to the event URL
        if (eventData?.url) {
          window.open(eventData.url, "_blank");
        }
      } else {
        setError(data.message || "Failed to save email");
      }
    } catch (err) {
      setError("An error occurred. Please try again.");
      console.error(err);
    } finally {
      setIsSubmitting(false);
      setOpen(false);
      setEmail("");
      setSuccess(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          {eventData ? (
            <DialogTitle className="text-lg md:text-2xl text-neutral-600 dark:text-neutral-100 font-bold text-center mb-4">
              Register for{" "}
              <span className="px-1 py-0.5 rounded-md bg-gray-100 dark:bg-neutral-800 dark:border-neutral-700 border border-gray-200">
                {eventData.title}
              </span>
            </DialogTitle>
          ) : (
            <DialogTitle>Register for Event</DialogTitle>
          )}
        </DialogHeader>

        {eventData ? (
          <>
            <div className="flex justify-center items-center">
              <motion.div
                style={{
                  rotate: Math.random() * 10 - 5,
                }}
                whileHover={{
                  scale: 1.05,
                  rotate: 0,
                  zIndex: 100,
                }}
                className="rounded-xl p-1 bg-white dark:bg-neutral-800 dark:border-neutral-700 border border-neutral-100 overflow-hidden"
              >
                <img
                  src={eventData.image}
                  alt={eventData.title}
                  width="500"
                  height="300"
                  className="rounded-lg h-40 w-full object-cover"
                />
              </motion.div>
            </div>
            <div className="py-4 flex flex-col gap-y-4 items-start justify-start max-w-sm mx-auto">
              <div className="flex items-center justify-center">
                <CalendarIcon className="mr-2 text-neutral-700 dark:text-neutral-300 h-4 w-4" />
                <span className="text-neutral-700 dark:text-neutral-300 text-sm">
                  {eventData.date}
                </span>
              </div>
              <div className="flex items-center justify-center">
                <LocationIcon className="mr-2 text-neutral-700 dark:text-neutral-300 h-4 w-4" />
                <span className="text-neutral-700 dark:text-neutral-300 text-sm">
                  {eventData.venue}
                </span>
              </div>
            </div>
            <div className="mt-2 mb-4">
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Enter your email to register
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={handleEmailChange}
                placeholder="your@email.com"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white dark:bg-gray-800"
                disabled={isSubmitting || success}
              />
              {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
              {success && (
                <p className="mt-2 text-sm text-green-600">
                  Registration successful!
                </p>
              )}
            </div>
          </>
        ) : (
          <p className="text-center">No event data available</p>
        )}

        <DialogFooter className="flex justify-end gap-2 mt-4">
          <button
            className="px-4 py-2 bg-gray-200 text-black dark:bg-black dark:border-black dark:text-white border border-gray-300 rounded-md text-sm"
            onClick={() => setOpen(false)}
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            className="px-4 py-2 bg-black text-white dark:bg-white dark:text-black text-sm rounded-md border border-black"
            onClick={handleSubmit}
            disabled={isSubmitting || success}
          >
            {isSubmitting
              ? "Submitting..."
              : success
              ? "Registered"
              : "Register"}
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

const CalendarIcon = ({ className }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  );
};

const LocationIcon = ({ className }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
      <circle cx="12" cy="10" r="3" />
    </svg>
  );
};
