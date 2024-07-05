import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import '@testing-library/jest-dom';

// 使用 vi.mock 全局模拟 react-router-dom，并确保 useNavigate 被正确模拟
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom'); // 导入所有实际的导出
  const navigate = vi.fn(); // 创建一个 mock 函数
  return {
    ...actual,
    useNavigate: () => navigate  // 返回模拟的 navigate 函数
  };
});

describe('SearchBar Component', () => {
  it('should render input element', () => {
    render(
      <MemoryRouter>
        <SearchBar />
      </MemoryRouter>
    );
    expect(screen.getByPlaceholderText('Search recipes')).toBeInTheDocument();
  });

  it('should allow entering text', async () => {
    render(
      <MemoryRouter>
        <SearchBar />
      </MemoryRouter>
    );
    const input = screen.getByPlaceholderText('Search recipes');
    await userEvent.type(input, 'Chicken');
  });

  it('should display an alert if search is attempted with empty input', async () => {
    render(
      <MemoryRouter>
        <SearchBar />
      </MemoryRouter>
    );
    const button = screen.getByRole('button', { name: 'Search' });
    fireEvent.click(button);
    expect(screen.getByText('Please enter a search term.')).toBeInTheDocument();
  });

  it('should navigate to search page on valid search', async () => {
    render(
      <MemoryRouter>
        <SearchBar />
      </MemoryRouter>
    );
    const input = screen.getByPlaceholderText('Search recipes');
    await userEvent.type(input, 'Chicken');
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' });
  });
});
