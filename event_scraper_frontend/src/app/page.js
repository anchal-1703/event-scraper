/* eslint-disable @next/next/no-img-element */
"use client";
import { useEffect, useState } from "react";
import { EventModal } from "@/components/home/EmailModal";
import {
  CardBadge,
  CardBody,
  CardContainer,
  CardItem,
} from "@/components/ui/3d-card";

export default function Home() {
  const [open, setOpen] = useState(false);
  const [eventData, setEventData] = useState([]);
  const [resData, setResData] = useState([]);

  const fetchEvents = async () => {
    const res = await fetch("/api/events");
    const data = await res.json();
    return data;
  };

  useEffect(() => {
    fetchEvents().then((res) => {
      setResData(res);
    });
  }, []);

  const handleOpen = (item) => {
    setEventData(item);
    setOpen(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-gray-50 to-gray-100 dark:from-[#0a0a0a] dark:via-[#111] dark:to-[#1a1a1a] text-gray-900 dark:text-gray-100 px-6 py-12 sm:px-12 lg:px-24 font-sans">
      <EventModal
        open={open}
        setOpen={setOpen}
        eventData={eventData}
        setEventData={setEventData}
      />

      <div className="max-w-8xl mx-auto text-center">
        <h1 className="text-4xl sm:text-5xl font-extrabold mb-4 tracking-tight">
          Discover the Best <span className="text-indigo-600 dark:text-indigo-400">Events in Sydney</span>
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
          Find trending and upcoming events happening around you. Get tickets, get notified, and never miss out.
        </p>

        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {resData["events"]?.map((item, index) => (
            <CardContainer key={index} className="inter-var">
              <CardBody className="bg-white dark:bg-[#121212] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 group/card p-8 flex flex-col justify-between h-full">
                {item.badge && (
                  <CardBadge className="bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300 font-medium text-xs px-2 py-1 rounded-full w-fit mb-2">
                    {item.badge}
                  </CardBadge>
                )}

                <CardItem
                  translateZ="50"
                  className="text-xl font-semibold text-gray-800 dark:text-white mb-2"
                >
                  {item.title}
                </CardItem>

                <div className="flex flex-col gap-1 mb-3">
                  <CardItem
                    as="p"
                    translateZ="60"
                    className="text-gray-600 dark:text-gray-400 text-sm"
                  >
                    📅 {item.date}
                  </CardItem>

                  <CardItem
                    as="p"
                    translateZ="60"
                    className="text-gray-600 dark:text-gray-400 text-sm"
                  >
                    📍 {item.venue}
                  </CardItem>
                </div>

                <CardItem translateZ="100" className="w-full overflow-hidden rounded-xl mb-4">
                  <img
                    src={item.image}
                    alt="event-thumbnail"
                    className="w-full h-52 object-cover transform group-hover/card:scale-105 transition duration-300 rounded-xl shadow"
                  />
                </CardItem>

                <CardItem
                  translateZ={20}
                  as="button"
                  className="mt-auto w-full text-center px-5 py-3 rounded-lg bg-indigo-600 text-white dark:bg-indigo-500 hover:bg-indigo-700 dark:hover:bg-indigo-600 transition-all duration-300 text-sm font-semibold tracking-wide"
                  onClick={() => handleOpen(item)}
                >
                  🎟️ Get Tickets
                </CardItem>
              </CardBody>
            </CardContainer>
          ))}
        </div>
      </div>
    </div>
  );
}
