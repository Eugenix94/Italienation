import { useState, useEffect } from 'react';

export const useIntersectionObserver = (refs, options = { threshold: 0.5 }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const observers = [];
    
    refs.forEach((ref, index) => {
      if (!ref.current) return;
      
      const observer = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
          setActiveIndex(index);
        }
      }, options);
      
      observer.observe(ref.current);
      observers.push(observer);
    });

    return () => {
      observers.forEach(observer => observer.disconnect());
    };
  }, [refs, options.threshold]);

  return activeIndex;
};
